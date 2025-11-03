# Supabase Setup Guide

This guide will help you set up Supabase authentication and database for the Kundli Calculator.

## Prerequisites

- A free Supabase account at [supabase.com](https://supabase.com)

## Step 1: Create a Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign in with GitHub (recommended) or email
4. Click "New Project"
5. Enter project details:
   - **Name:** Kundli Calculator (or your preferred name)
   - **Database Password:** Create a strong password (save it!)
   - **Region:** Choose closest to your users
   - **Pricing Plan:** Free (perfect for getting started!)
6. Click "Create new project"
7. Wait 2-3 minutes for project to be ready

## Step 2: Get API Credentials

1. In your Supabase project dashboard, go to **Project Settings** (⚙️ icon in sidebar)
2. Click **API** in the left menu
3. You'll see two important values:
   - **Project URL** (e.g., `https://abcdefgh.supabase.co`)
   - **anon public key** (a long string starting with `eyJ...`)

## Step 3: Update .env.local

1. Open `frontend/next-app/.env.local`
2. Replace the placeholder values:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=https://your-actual-project-id.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
3. Save the file

## Step 4: Create Database Schema

1. In your Supabase project dashboard, click **SQL Editor** in the sidebar
2. Click **New query**
3. Copy and paste the entire contents of `supabase_schema.sql` from the project root
4. Click **Run** (or press Ctrl+Enter)
5. You should see "Success. No rows returned" - that's good!

## Step 5: Configure Authentication

1. In Supabase dashboard, go to **Authentication** > **Providers**
2. Enable **Email** provider (should be enabled by default)
3. Optional: Configure email templates
   - Go to **Authentication** > **Email Templates**
   - Customize the confirmation email if desired

## Step 6: Test Authentication

1. Start your frontend: `cd frontend/next-app && npm run dev`
2. Open [http://localhost:3100](http://localhost:3100)
3. Click "Sign Up" in the header
4. Create a test account
5. Check your email for the confirmation link
6. Click the link to verify your email
7. Log in with your credentials

## Step 7: Test Chart Saving

1. Log in to your account
2. Fill in the birth details form
3. Click "Generate Kundli"
4. After the chart loads, click "💾 Save Chart"
5. Enter a title and click "Save Chart"
6. Check Supabase dashboard:
   - Go to **Table Editor** > **charts**
   - You should see your saved chart!

## Troubleshooting

### "User not authenticated" error
- Make sure you're logged in
- Check that `.env.local` has the correct Supabase credentials
- Try refreshing the page

### Email confirmation not received
- Check spam folder
- In Supabase dashboard, go to **Authentication** > **Users**
- Find your user and manually confirm the email by clicking the user

### Database errors
- Make sure you ran the `supabase_schema.sql` script completely
- Check **Database** > **Tables** to verify `charts` table exists
- Verify Row Level Security (RLS) is enabled

### CORS errors
- This shouldn't happen with Supabase, but if it does:
- Check that your Supabase URL is correct
- Make sure you're using the `anon` key, not the `service_role` key

## What's Next?

Your Kundli Calculator now has:
- ✅ User authentication (email/password)
- ✅ Secure chart storage (per-user)
- ✅ Row Level Security (users can only see their own charts)

Next features you can add:
- View saved charts list
- Edit/delete saved charts
- Share charts with others
- Add more authentication providers (Google, Facebook, etc.)

## Free Tier Limits

Supabase Free Tier includes:
- **500 MB database space** (~10,000 charts)
- **2 GB bandwidth/month** (~20,000 requests)
- **50 MB file storage**
- **50,000 monthly active users**

This is more than enough for getting started! 🚀
