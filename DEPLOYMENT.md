# 🚀 ParGaMD GUI Deployment Guide

## Streamlit Community Cloud Deployment (Recommended)

### Prerequisites
- GitHub repository with your code
- GitHub account
- Streamlit Community Cloud account

### Steps to Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Community Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `your-username/ParGaMD-GUI`
   - Main file path: `streamlit_app.py`
   - App URL: Choose a unique name
   - Click "Deploy!"

3. **Configuration**
   - The app will automatically use `requirements.txt`
   - Configuration from `.streamlit/config.toml` will be applied
   - Environment variables can be set in the Streamlit dashboard

### Local Testing Before Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run streamlit_app.py

# Test all features
# - File upload
# - CV selection
# - Configuration generation
# - Live editing
# - ZIP download
```

## Alternative Deployment Options

### Heroku
1. Create `Procfile`: `web: streamlit run streamlit_app.py --server.port=$PORT`
2. Deploy via Heroku CLI or GitHub integration

### Railway
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `streamlit run streamlit_app.py --server.port=$PORT`

### Docker (Advanced)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

## Troubleshooting

### Common Issues
- **Import errors**: Check `requirements.txt` has all dependencies
- **File not found**: Ensure all template files are included
- **Memory issues**: Optimize file reading in production

### Performance Tips
- Use `st.cache_data` for expensive operations
- Optimize file upload handling
- Consider file size limits

## Environment Variables

Set these in Streamlit Community Cloud dashboard:
- `STREAMLIT_SERVER_PORT=8501`
- `STREAMLIT_SERVER_ADDRESS=0.0.0.0`

## Support

For deployment issues:
1. Check Streamlit Community Cloud logs
2. Test locally first
3. Verify all dependencies are in requirements.txt
