# Production Deployment Guide

This project is prepared for this production architecture:

```text
Frontend (Vercel)
  -> HTTPS API requests
Backend API (Render)
  -> MongoDB Atlas
```

## Deployment Blockers Fixed

- Frontend API calls no longer hardcode a localhost backend.
- Vite reads the backend URL from `VITE_API_URL`.
- Backend CORS is controlled by `ALLOWED_ORIGINS` instead of allowing every origin in production.
- MongoDB credentials stay in environment variables and are not committed.
- Backend has a WSGI entrypoint for Gunicorn/Render.
- Render and Vercel deployment config files are included.
- MongoDB seed data no longer deletes and recreates production collections on every startup.

## Environment Variables

### Frontend: Vercel

Set this in the Vercel project settings:

```text
VITE_API_URL=https://your-render-service.onrender.com/api
```

Vite only exposes client-side environment variables with the `VITE_` prefix. Do not put secrets in frontend variables because they are visible in the browser bundle.

### Backend: Render

Set these in the Render service settings:

```text
MONGODB_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/?appName=BankCluster
MONGODB_DB_NAME=BankCluster
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
FLASK_ENV=production
SEED_DATABASE=false
```

For multiple frontend domains, separate origins with commas:

```text
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app,https://www.yourdomain.com
```

## Backend Deployment: Render

1. Push the repository to GitHub.
2. In Render, create a new Web Service from the repo.
3. Use the included `render.yaml` blueprint, or configure manually:
   - Root Directory: `BankAPI`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app --bind 0.0.0.0:$PORT`
4. Add the backend environment variables listed above.
5. Deploy the service.
6. Test:

```bash
curl https://your-render-service.onrender.com/health
curl https://your-render-service.onrender.com/api/customers
```

## MongoDB Atlas Configuration

1. Rotate any database password that was ever committed or pushed.
2. In Atlas, create a database user with the minimum permissions this app needs.
3. Add the Render outbound IPs to Atlas Network Access, or temporarily allow all access with `0.0.0.0/0`.
4. Store the connection string only in Render as `MONGODB_URI`.
5. Leave `SEED_DATABASE=false` for production unless you intentionally want sample records inserted into an empty database.

## Frontend Deployment: Vercel

1. In Vercel, import the GitHub repository.
2. Set the project root directory to `frontend`.
3. Vercel should use:
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Add:

```text
VITE_API_URL=https://your-render-service.onrender.com/api
```

5. Deploy.
6. Open the Vercel URL and test customer/account CRUD operations.

## Domain Configuration

1. Add the custom frontend domain in Vercel.
2. Add the final frontend origin to Render:

```text
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app,https://www.yourdomain.com
```

3. Redeploy or restart the Render backend after changing CORS settings.
4. If the backend has a custom domain, update Vercel:

```text
VITE_API_URL=https://api.yourdomain.com/api
```

Then redeploy the frontend because Vite environment variables are built into the static bundle.

## Final Testing Checklist

- Backend `/health` returns `200`.
- Backend `/api/customers` returns JSON from Render.
- MongoDB Atlas shows successful connections from Render.
- Vercel app loads over HTTPS.
- Browser network tab shows requests going to the Render backend, not localhost.
- No CORS errors appear in the browser console.
- Create, edit, search, and delete flows work for customers and accounts.
- `.env` files are not tracked by Git.
- Production secrets exist only in Vercel/Render dashboards.

## Remaining Production Considerations

- The API currently has no authentication. Anyone allowed by CORS can use the CRUD endpoints from a browser, and non-browser clients can call the API directly.
- Render free-tier services may sleep, causing the first API request after inactivity to be slow.
- If this app will hold real banking data, add authentication, authorization, audit logging, input validation hardening, rate limiting, and HTTPS-only custom domains before launch.
