# Troubleshooting Guide

## What to Check

### 1. Are you logged in?
- Go to your app in the browser
- Check if you see your username/profile
- If not logged in, log in first
- Then go to Interview Prep page

### 2. Is the React dev server running?
Open a terminal and run:
```bash
cd c:\Users\DELL\career_assistant_project\career-assistant-frontend
npm start
```

Wait for "Compiled successfully!" message.

### 3. Check browser console
- Press F12 in your browser
- Go to Console tab
- Look for any errors (red text)
- Look for the message: "Failed to check resume:"

### 4. Hard refresh
- Press Ctrl + Shift + R
- Or Ctrl + F5
- This clears cache

### 5. Check what you're seeing
Take a screenshot or describe:
- What text is showing on Interview Prep page?
- Is there a yellow/orange box?
- What buttons do you see?

## Expected Behavior

### If NOT logged in:
- Should redirect to login page
- OR show error about authentication

### If logged in but NO resume:
- Should see yellow/orange box
- Text: "Resume Required for Personalized Interview"
- Button: "📤 Upload Resume Now"
- Button: "🔄 I Already Uploaded"

### If logged in WITH resume:
- No yellow box
- Can select domain and start interview

## Quick Test

1. Open browser console (F12)
2. Go to Interview Prep page
3. Type this in console:
```javascript
localStorage.getItem('authToken')
```
4. If it returns `null`, you're not logged in
5. If it returns a long string, you ARE logged in

## Next Steps

Based on what you see, we can fix the specific issue!
