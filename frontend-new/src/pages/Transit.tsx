import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Grid,
  TextField,
  Button,
  Box,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  Chip,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import KundliChart from '../components/charts/KundliChart';
import { kundliApi } from '../services/api';

interface TransitAnalysis {
  date: string;
  aspects: {
    planet1: string;
    planet2: string;
    aspect: string;
    nature: 'beneficial' | 'challenging' | 'neutral';
    description: string;
  }[];
  predictions: {
    domain: string;
    description: string;
    strength: number;
  }[];
  periodInfo: {
    dasha: string;
    antardasha: string;
    pratyantardasha: string;
  };
}

const TransitPage: React.FC = () => {
  const [transitDate, setTransitDate] = useState<Date | null>(new Date());
  const [transitTime, setTransitTime] = useState<Date | null>(new Date());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [transitData, setTransitData] = useState<TransitAnalysis | null>(null);
  const [birthChart, setBirthChart] = useState<any>(null);
  const [transitChart, setTransitChart] = useState<any>(null);

  const handleAnalyze = async () => {
    if (!transitDate || !transitTime) {
      setError('Please select both date and time');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await kundliApi.calculateTransit({
        date: transitDate.toISOString().split('T')[0],
        time: transitTime.toISOString().split('T')[1].substring(0, 8),
        latitude: 0, // Use saved birth chart details
        longitude: 0,
        timezone: 'UTC',
        ayanamsa: 'LAHIRI',
        houseSystem: 'PLACIDUS',
      });

      setTransitData(response.analysis);
      setBirthChart(response.birthChart);
      setTransitChart(response.transitChart);
    } catch (err) {
      setError('Failed to calculate transit analysis. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getAspectColor = (nature: string) => {
    switch (nature) {
      case 'beneficial':
        return 'success';
      case 'challenging':
        return 'error';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '60vh',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container>
      <Paper elevation={3} sx={{ mt: 3, p: 3 }}>
        <Typography variant="h4" gutterBottom align="center">
          Transit Analysis
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <LocalizationProvider dateAdapter={AdapterDateFns}>
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} md={6}>
              <DatePicker
                label="Transit Date"
                value={transitDate}
                onChange={(newValue) => setTransitDate(newValue)}
                sx={{ width: '100%' }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TimePicker
                label="Transit Time"
                value={transitTime}
                onChange={(newValue) => setTransitTime(newValue)}
                sx={{ width: '100%' }}
              />
            </Grid>
          </Grid>
        </LocalizationProvider>

        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <Button
            variant="contained"
            onClick={handleAnalyze}
            size="large"
            sx={{ minWidth: 200 }}
          >
            Analyze Transit
          </Button>
        </Box>

        {transitData && (
          <>
            <Grid container spacing={4}>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Birth Chart
                </Typography>
                {birthChart && (
                  <KundliChart
                    planets={birthChart.planets}
                    houses={birthChart.houses}
                  />
                )}
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Transit Chart
                </Typography>
                {transitChart && (
                  <KundliChart
                    planets={transitChart.planets}
                    houses={transitChart.houses}
                  />
                )}
              </Grid>
            </Grid>

            <Box sx={{ mt: 4 }}>
              <Typography variant="h5" gutterBottom>
                Current Period
              </Typography>
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={4}>
                      <Typography variant="subtitle2">Maha Dasha</Typography>
                      <Typography variant="body1">
                        {transitData.periodInfo.dasha}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <Typography variant="subtitle2">Antar Dasha</Typography>
                      <Typography variant="body1">
                        {transitData.periodInfo.antardasha}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <Typography variant="subtitle2">Pratyantar Dasha</Typography>
                      <Typography variant="body1">
                        {transitData.periodInfo.pratyantardasha}
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>

              <Typography variant="h5" gutterBottom>
                Transit Aspects
              </Typography>
              <Grid container spacing={2}>
                {transitData.aspects.map((aspect, index) => (
                  <Grid item xs={12} key={index}>
                    <Card>
                      <CardContent>
                        <Box
                          sx={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            mb: 1,
                          }}
                        >
                          <Typography variant="h6">
                            {aspect.planet1} {aspect.aspect} {aspect.planet2}
                          </Typography>
                          <Chip
                            label={aspect.nature}
                            color={getAspectColor(aspect.nature)}
                            size="small"
                          />
                        </Box>
                        <Typography variant="body2">
                          {aspect.description}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>

              <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
                Predictions
              </Typography>
              <Grid container spacing={2}>
                {transitData.predictions.map((prediction, index) => (
                  <Grid item xs={12} md={6} key={index}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          {prediction.domain}
                        </Typography>
                        <Typography variant="body2" paragraph>
                          {prediction.description}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Strength: {prediction.strength}/10
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Box>
          </>
        )}
      </Paper>
    </Container>
  );
};

export default TransitPage;
