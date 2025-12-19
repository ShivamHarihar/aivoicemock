# Debugging Guide for Interview Results Dashboard

## Issue: "Unable to Load Results - Failed to fetch results"

### Steps to Debug:

1. **Open Browser Console (F12)**
   - Navigate to the Results page after completing an interview
   - Open Developer Tools (F12)
   - Go to the Console tab
   - Look for error messages

2. **Check the Console Logs**
   You should see logs like:
   ```
   Loading results for session: <session_id>
   Fetching from: /api/interview_results/<session_id>
   Response status: <status_code>
   Response OK: <true/false>
   ```

3. **Common Issues and Solutions:**

   **A. Session Not Found (404 Error)**
   - **Symptom**: Console shows "Response status: 404"
   - **Cause**: Session ID doesn't exist in memory
   - **Solution**: Check if the interview actually completed and created a session
   
   **B. Server Error (500 Error)**
   - **Symptom**: Console shows "Response status: 500"
   - **Cause**: Backend error while processing results
   - **Check**: Look at the terminal running `python app.py` for error stack traces
   
   **C. Network Error**
   - **Symptom**: Console shows "Failed to fetch"
   - **Cause**: Server not running or network issue
   - **Solution**: Ensure `python app.py` is running on port 5000

4. **Manual API Test**
   Open a new browser tab and navigate to:
   ```
   http://localhost:5000/api/interview_results/<your_session_id>
   ```
   Replace `<your_session_id>` with the actual session ID from the URL.
   
   You should see JSON data like:
   ```json
   {
     "session_id": "abc123",
     "overall_score": 50,
     "mode": "HR",
     ...
   }
   ```

5. **Check Server Logs**
   In the terminal running `python app.py`, you should see:
   ```
   Fetching results for session: <session_id>
   Session found. Keys: dict_keys([...])
   Session data - Scores: X, Analyses: Y, History: Z
   Successfully generated results for session <session_id>
   ```

6. **Quick Fix: Test with a Fresh Interview**
   - Go to http://localhost:5000/dashboard
   - Start a new interview
   - Answer at least one question
   - Wait for the interview to complete (or manually end it)
   - Check if the results page loads correctly

### Expected Behavior:

When working correctly:
1. Interview completes → Redirects to `/result?session_id=<id>`
2. Results page loads → Shows loading spinner
3. API call to `/api/interview_results/<id>` → Returns JSON data
4. Dashboard displays → Shows animated score, metrics, charts

### If Still Not Working:

**Check these files:**
- `backend/app/app.py` - API endpoint at line ~492
- `frontend/src/result.html` - JavaScript at line ~420
- `backend/src/memory_store.py` - Session storage

**Verify:**
- Flask server is running without errors
- Session is created when interview starts
- Session persists until results page loads
- API endpoint is accessible

### Test Command:

Run this in PowerShell to test the API directly:
```powershell
# Replace SESSION_ID with your actual session ID
$sessionId = "your_session_id_here"
Invoke-WebRequest -Uri "http://localhost:5000/api/interview_results/$sessionId" -Method GET
```

This will show you the raw API response and help identify the issue.
