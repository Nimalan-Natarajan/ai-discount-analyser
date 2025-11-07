# 🚨 **403 ERROR DURING FILE UPLOAD - TROUBLESHOOTING GUIDE**

## **What is a 403 Error?**
A 403 "Forbidden" error during file upload typically indicates:
- **Browser security restrictions**
- **CORS (Cross-Origin Resource Sharing) issues**
- **File permission problems**
- **Network/proxy blocking**
- **Streamlit server configuration issues**

---

## **🔧 IMMEDIATE FIXES TO TRY**

### **Fix 1: Browser Cache & Refresh**
```bash
1. Hard refresh: Ctrl + Shift + R (Windows) or Cmd + Shift + R (Mac)
2. Clear browser cache for localhost
3. Try incognito/private browsing mode
4. Try different browser (Chrome/Firefox/Edge)
```

### **Fix 2: Restart Streamlit Completely**
```bash
# In PowerShell/Terminal:
1. Close browser
2. Stop Streamlit (Ctrl+C in terminal)
3. Wait 10 seconds
4. Restart: streamlit run src/app.py
5. Open fresh browser tab
```

### **Fix 3: Check File Permissions**
```bash
# Ensure your CSV file has read permissions
# Try copying test_quotes.csv to desktop and upload from there
```

### **Fix 4: File Size & Format Check**
- **Max file size**: Keep under 5MB for testing
- **File format**: Ensure it's actually a .csv file
- **File encoding**: Save as UTF-8 encoding

---

## **🔍 DEBUGGING STEPS**

### **Step 1: Verify Your File Format**
Your `test_quotes.csv` should have exactly these columns:
```
date,customerName,shipmentType,commodityType,shipperCountry,shipperStation,consigneeCountry,consigneeStation,discount,accepted
```

### **Step 2: Check Browser Developer Tools**
1. Open browser DevTools (F12)
2. Go to Network tab
3. Try uploading file
4. Look for failed requests (red entries)
5. Check error details

### **Step 3: Test with Small File**
Create a minimal test file with just 2 rows:
```csv
date,customerName,shipmentType,commodityType,shipperCountry,shipperStation,consigneeCountry,consigneeStation,discount,accepted
1/1/2025,Test Corp,AIR,General,USA,LAX,UK,LHR,10,TRUE
1/2/2025,Test Corp,AIR,General,USA,LAX,UK,LHR,12,FALSE
```

---

## **🚀 ALTERNATIVE UPLOAD METHODS**

### **Method 1: Direct File Placement**
```bash
# Copy your file directly to the project folder:
# Place test_quotes.csv in: DiscountPredictor/
# The app will auto-detect and load it
```

### **Method 2: Use Sample Data Button** (if available)
```bash
# Use the built-in sample data to test functionality first
```

---

## **⚡ QUICK RESOLUTION STEPS**

1. **🔄 Restart Everything**: Close browser → Stop Streamlit → Restart → Fresh browser
2. **🗂️ File Check**: Verify file is valid CSV with correct columns
3. **🌐 Browser Test**: Try different browser or incognito mode
4. **📁 Local Copy**: Copy CSV to project root directory instead of uploading

---

## **💡 LIKELY CAUSES & SOLUTIONS**

| **Cause** | **Solution** |
|-----------|-------------|
| Browser cache | Hard refresh (Ctrl+Shift+R) |
| CORS policy | Restart Streamlit server |
| File permissions | Copy file to desktop, upload from there |
| Large file size | Use smaller test file (< 1MB) |
| Network proxy | Try different network or disable proxy |
| Antivirus blocking | Temporarily disable real-time protection |

---

## **🎯 IF NOTHING WORKS**

**Try this emergency workaround:**
1. Copy your `test_quotes.csv` to the project root folder
2. Rename it to `uploaded_data.csv`  
3. Modify the app to auto-load this file on startup
4. This bypasses the upload mechanism entirely

**Still having issues?** 
- Share the exact error message from browser DevTools
- Try the minimal 2-row test file above
- Check if other Streamlit features work (navigation, buttons, etc.)

---

## **✅ SUCCESS INDICATORS**
When upload works correctly, you should see:
- ✅ "File uploaded: filename.csv (X bytes)"
- ✅ "🔄 Processing your data..."
- ✅ "Data processed successfully! Loaded X records."
- ✅ Data summary with metrics displayed
