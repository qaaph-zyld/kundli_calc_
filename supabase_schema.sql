-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create charts table
CREATE TABLE IF NOT EXISTS public.charts (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  title VARCHAR(255) NOT NULL,
  birth_details JSONB NOT NULL,
  chart_data JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()) NOT NULL
);

-- Create index on user_id for faster queries
CREATE INDEX IF NOT EXISTS idx_charts_user_id ON public.charts(user_id);

-- Create index on created_at for sorting
CREATE INDEX IF NOT EXISTS idx_charts_created_at ON public.charts(created_at DESC);

-- Enable Row Level Security
ALTER TABLE public.charts ENABLE ROW LEVEL SECURITY;

-- Create policy: Users can only see their own charts
CREATE POLICY "Users can view own charts" ON public.charts
  FOR SELECT
  USING (auth.uid() = user_id);

-- Create policy: Users can insert their own charts
CREATE POLICY "Users can insert own charts" ON public.charts
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Create policy: Users can update their own charts
CREATE POLICY "Users can update own charts" ON public.charts
  FOR UPDATE
  USING (auth.uid() = user_id);

-- Create policy: Users can delete their own charts
CREATE POLICY "Users can delete own charts" ON public.charts
  FOR DELETE
  USING (auth.uid() = user_id);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = TIMEZONE('utc', NOW());
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_charts_updated_at BEFORE UPDATE ON public.charts
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
