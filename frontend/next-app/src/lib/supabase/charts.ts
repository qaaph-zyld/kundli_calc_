import { createClient } from './client';
import { BirthDetails } from '../../components/BirthDetailsForm';

export interface SavedChart {
  id: string;
  user_id: string;
  title: string;
  birth_details: BirthDetails;
  chart_data: any;
  created_at: string;
  updated_at: string;
}

export async function saveChart(
  title: string,
  birthDetails: BirthDetails,
  chartData: any
): Promise<{ data: SavedChart | null; error: any }> {
  const supabase = createClient();
  
  const { data: { user } } = await supabase.auth.getUser();
  
  if (!user) {
    return { data: null, error: { message: 'User not authenticated' } };
  }

  const { data, error } = await supabase
    .from('charts')
    .insert({
      user_id: user.id,
      title,
      birth_details: birthDetails,
      chart_data: chartData,
    })
    .select()
    .single();

  return { data, error };
}

export async function getUserCharts(): Promise<{ data: SavedChart[] | null; error: any }> {
  const supabase = createClient();
  
  const { data: { user } } = await supabase.auth.getUser();
  
  if (!user) {
    return { data: null, error: { message: 'User not authenticated' } };
  }

  const { data, error } = await supabase
    .from('charts')
    .select('*')
    .eq('user_id', user.id)
    .order('created_at', { ascending: false });

  return { data, error };
}

export async function getChart(chartId: string): Promise<{ data: SavedChart | null; error: any }> {
  const supabase = createClient();

  const { data, error } = await supabase
    .from('charts')
    .select('*')
    .eq('id', chartId)
    .single();

  return { data, error };
}

export async function updateChart(
  chartId: string,
  updates: Partial<Pick<SavedChart, 'title' | 'birth_details' | 'chart_data'>>
): Promise<{ data: SavedChart | null; error: any }> {
  const supabase = createClient();

  const { data, error } = await supabase
    .from('charts')
    .update(updates)
    .eq('id', chartId)
    .select()
    .single();

  return { data, error };
}

export async function deleteChart(chartId: string): Promise<{ error: any }> {
  const supabase = createClient();

  const { error } = await supabase
    .from('charts')
    .delete()
    .eq('id', chartId);

  return { error };
}
