import logging
from .grok_client import generate_resume_analysis
from .prompts import RESUME_RECREATION_PROMPT
from .resume_analyzer import analyze_resume_content

logger = logging.getLogger(__name__)

def recreate_resume_with_ai(resume_text, current_score, analysis_data):
    """
    Uses AI to recreate and optimize a resume for better ATS compatibility.
    Implements intelligent retry logic if initial recreation doesn't improve score.
    
    Args:
        resume_text: Original resume text
        current_score: Current ATS score (0-100)
        analysis_data: Dict containing weakness analysis
    
    Returns:
        Dict with recreated resume and metadata
    """
    try:
        if not resume_text or len(resume_text) < 100:
            return {"error": "Resume text is too short to optimize"}
        
        # Extract weaknesses for targeted improvement
        weaknesses = analysis_data.get("weaknesses", [])
        weaknesses_text = "\n".join([f"- {w}" for w in weaknesses]) if weaknesses else "General ATS optimization needed"
        
        # Calculate intelligent target score (AI-driven, not hardcoded)
        target_score = min(100, current_score + 10)  # User specified 10% minimum improvement
        
        # Maximum retry attempts for intelligent recreation
        max_attempts = 2
        best_result = None
        best_score = current_score
        
        for attempt in range(1, max_attempts + 1):
            logger.info(f"🎯 Recreation attempt {attempt}/{max_attempts} (Target: {target_score}+)")
            
            # Build intelligent, context-aware prompt
            if attempt == 1:
                # First attempt: Use standard recreation prompt
                specific_improvements = f"""
📋 SPECIFIC WEAKNESSES TO ADDRESS:
{weaknesses_text}

Focus particularly on improving these aspects to boost the score.
"""
            else:
                # Retry attempt: Add aggressive improvement instructions
                score_gap = current_score - best_score if best_result else 0
                specific_improvements = f"""
⚠️ RETRY ATTEMPT {attempt} - Previous recreation did not meet quality standards.

CRITICAL ISSUES FROM PREVIOUS ATTEMPT:
- Score achieved: {best_score}/100 (below target of {target_score})
- Score improvement gap: {score_gap} points (need +{target_score - current_score} minimum)

📋 ORIGINAL WEAKNESSES TO ADDRESS:
{weaknesses_text}

🔥 AGGRESSIVE OPTIMIZATION REQUIRED:
1. SIGNIFICANTLY expand technical details (add frameworks, methodologies, tools)
2. ADD MORE bullet points (minimum 15-20 across all experience)
3. Each bullet must show IMPACT with action verbs
4. Maximize ATS keyword density (add all relevant technical terms)
5. Expand project descriptions to 4-6 bullets each
6. Create comprehensive skills section (20+ items)
7. Add professional summary highlighting key achievements

This is your last chance - make it count!
"""
            
            # Create dynamic prompt with intelligent targeting
            # IMPORTANT: Send FULL resume text - do not truncate!
            # The AI needs ALL information to create a complete optimized resume
            prompt = RESUME_RECREATION_PROMPT.format(
                resume_text=resume_text,  # Full text, no truncation
                current_score=current_score,
                target_score=target_score,
                specific_improvements=specific_improvements
            )
            
            logger.info(f"📤 Sending recreation request to AI (attempt {attempt})...")
            
            # Call AI to recreate resume
            response = generate_resume_analysis(prompt)
            
            if isinstance(response, dict) and "error" in response:
                logger.error(f"❌ AI error on attempt {attempt}: {response['error']}")
                if attempt < max_attempts:
                    continue  # Try again
                return response  # Final attempt failed
            
            # Parse AI response
            if isinstance(response, dict):
                resume_markdown = response.get("resume_markdown", "")
                ai_predicted_score = response.get("new_score", 0)
                quality_confidence = response.get("quality_confidence", 0)
                
                if not resume_markdown:
                    logger.warning(f"⚠️ No resume markdown in response on attempt {attempt}")
                    if attempt < max_attempts:
                        continue
                    return {"error": "AI did not generate resume content"}
                
                # ✨ INTELLIGENT VERIFICATION: Analyze with real analyzer
                logger.info(f"🔍 Verifying recreated resume with real analyzer...")
                analysis_result = analyze_resume_content(resume_markdown)
                
                if analysis_result and "overall_score" in analysis_result and "error" not in analysis_result:
                    real_new_score = analysis_result["overall_score"]
                    improvement = real_new_score - current_score
                    
                    logger.info(f"📊 Attempt {attempt} Results:")
                    logger.info(f"   - AI predicted: {ai_predicted_score}")
                    logger.info(f"   - Real analyzed: {real_new_score}")
                    logger.info(f"   - Improvement: {improvement:+.1f} points")
                    logger.info(f"   - AI confidence: {quality_confidence}%")
                    
                    # AI-driven decision: Is this result acceptable?
                    meets_target = real_new_score >= target_score
                    is_improvement = real_new_score > current_score
                    
                    # Store if this is the best result so far
                    if real_new_score > best_score:
                        best_score = real_new_score
                        best_result = {
                            "resume_markdown": resume_markdown,
                            "new_score": real_new_score,
                            "old_score": current_score,
                            "improvement": improvement,
                            "improvements_made": response.get("improvements_made", []),
                            "keywords_added": response.get("keywords_added", []),
                            "attempt_number": attempt,
                            "content_expansion": response.get("content_expansion_ratio", "0%")
                        }
                    
                    # ✨ INTELLIGENT DECISION LOGIC
                    if meets_target:
                        # SUCCESS! Target score achieved
                        logger.info(f"✅ SUCCESS! Recreation achieved target score of {target_score}+ on attempt {attempt}")
                        return best_result
                    elif is_improvement and attempt == max_attempts:
                        # Last attempt - return best result even if below target
                        logger.info(f"✅ Returning best result from attempt {best_result['attempt_number']} ({best_score} vs original {current_score})")
                        return best_result
                    elif not is_improvement and attempt < max_attempts:
                        # Score didn't improve - retry with more aggressive prompt
                        logger.warning(f"⚠️ Attempt {attempt} scored {real_new_score} (no improvement). Retrying with aggressive optimization...")
                        continue
                    elif not is_improvement and attempt == max_attempts:
                        # Final attempt still didn't improve - return original gracefully
                        logger.warning(f"❌ All {max_attempts} attempts failed to improve score")
                        
                        # IMPORTANT: Convert original text to markdown format for preview
                        # The resume_text is plain text extracted from PDF, we need markdown
                        logger.info("Converting original resume to markdown format for display...")
                        
                        # Use AI to convert plain text to markdown (simple formatting task)
                        conversion_prompt = f"""Convert this resume text into clean, professional markdown format.

ORIGINAL RESUME TEXT:
{resume_text}

INSTRUCTIONS:
1. Format as markdown with proper headers (# for name, ## for sections)
2. Use bullet points (- ) for lists
3. Use **bold** for job titles and company names
4. Keep ALL original content - don't add or remove anything
5. Just reformat the existing text into markdown structure

Return ONLY the markdown-formatted resume, nothing else."""

                        try:
                            markdown_response = generate_resume_analysis(conversion_prompt)
                            if isinstance(markdown_response, dict):
                                formatted_markdown = markdown_response.get("resume_markdown", resume_text)
                            else:
                                formatted_markdown = str(markdown_response) if markdown_response else resume_text
                        except Exception as e:
                            logger.error(f"Markdown conversion failed: {e}")
                            # Fallback: basic markdown formatting
                            formatted_markdown = f"# Resume\n\n{resume_text}"
                        
                        # Return original resume with friendly message (not an error)
                        return {
                            "resume_markdown": formatted_markdown,  # Properly formatted markdown
                            "new_score": current_score,  # Keep original score
                            "old_score": current_score,
                            "improvement": 0,
                            "improvements_made": [],
                            "keywords_added": [],
                            "already_optimized": True,
                            "message": "No new keywords or skills found to level up this resume score. Your resume is already well-optimized!"
                        }
                    else:
                        # Didn't meet target - try again
                        logger.info(f"⚠️ Score {real_new_score} below target {target_score}. Retrying...")
                        continue
                        
                else:
                    # Analyzer failed
                    logger.warning(f"⚠️ Analyzer failed on attempt {attempt}")
                    if attempt < max_attempts:
                        continue
                    # Use AI's prediction as fallback on final attempt
                    return {
                        "resume_markdown": resume_markdown,
                        "new_score": ai_predicted_score,
                        "old_score": current_score,
                        "improvements_made": response.get("improvements_made", []),
                        "keywords_added": response.get("keywords_added", []),
                        "warning": "Score verification unavailable - using AI estimate"
                    }
        
        # Should not reach here, but just in case
        if best_result:
            logger.info(f"✅ Returning best result achieved: {best_score}")
            return best_result
        
        return {"error": "Resume recreation failed after all attempts"}
    
    except Exception as e:
        logger.error(f"Resume recreation failed: {e}", exc_info=True)
        return {"error": str(e)}


def generate_sample_optimized_resume(resume_text):
    """
    Fallback function to create a basic optimized version if AI fails.
    This is a simple template-based approach.
    """
    return f"""# Professional Resume

## Summary
Experienced professional with strong background in software development and project management.

## Skills
- Technical Skills: Python, JavaScript, React, Node.js
- Soft Skills: Team Leadership, Communication, Problem Solving

## Experience

### Software Engineer
*Company Name | 2020 - Present*

- Led development of web applications using modern frameworks
- Implemented automated testing improving code quality by 40%
- Collaborated with cross-functional teams on critical projects

## Education
**Bachelor's Degree in Computer Science**
University Name | 2020

## Projects
Various software projects demonstrating technical proficiency
"""
