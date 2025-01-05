import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Box,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Timeline,
  Person,
  Work,
  Favorite,
  LocalHospital,
  AttachMoney,
} from '@mui/icons-material';
import { kundliApi } from '../services/api';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`prediction-tabpanel-${index}`}
      aria-labelledby={`prediction-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

interface Prediction {
  domain: string;
  description: string;
  probability: number;
  timing?: {
    start: string;
    duration: number;
  };
  strength: number;
}

const PredictionsPage: React.FC = () => {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tabValue, setTabValue] = useState(0);

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        setLoading(true);
        setError(null);
        // Replace with actual kundli ID
        const response = await kundliApi.generatePredictions('latest');
        setPredictions(response.predictions);
      } catch (err) {
        setError('Failed to load predictions. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchPredictions();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const getDomainIcon = (domain: string) => {
    switch (domain.toLowerCase()) {
      case 'career':
        return <Work />;
      case 'relationship':
        return <Favorite />;
      case 'health':
        return <LocalHospital />;
      case 'finance':
        return <AttachMoney />;
      default:
        return <Person />;
    }
  };

  const formatPredictionTiming = (timing?: { start: string; duration: number }) => {
    if (!timing) return 'No timing information available';
    const start = new Date(timing.start);
    const duration = timing.duration;
    return `From ${start.toLocaleDateString()} for ${duration} days`;
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

  if (error) {
    return (
      <Container>
        <Alert severity="error" sx={{ mt: 3 }}>
          {error}
        </Alert>
      </Container>
    );
  }

  return (
    <Container>
      <Paper elevation={3} sx={{ mt: 3, p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Your Predictions
        </Typography>

        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            aria-label="prediction domains"
          >
            <Tab icon={<Timeline />} label="All" />
            <Tab icon={<Work />} label="Career" />
            <Tab icon={<Favorite />} label="Relationships" />
            <Tab icon={<LocalHospital />} label="Health" />
            <Tab icon={<AttachMoney />} label="Finance" />
          </Tabs>
        </Box>

        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={3}>
            {predictions.map((prediction, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      {getDomainIcon(prediction.domain)}
                      <Typography
                        variant="h6"
                        component="div"
                        sx={{ ml: 1 }}
                      >
                        {prediction.domain}
                      </Typography>
                    </Box>
                    <Typography variant="body1" paragraph>
                      {prediction.description}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Probability: {(prediction.probability * 100).toFixed(1)}%
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Timing: {formatPredictionTiming(prediction.timing)}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>

        {['Career', 'Relationships', 'Health', 'Finance'].map((domain, index) => (
          <TabPanel value={tabValue} index={index + 1} key={domain}>
            <Grid container spacing={3}>
              {predictions
                .filter((p) => p.domain.toLowerCase() === domain.toLowerCase())
                .map((prediction, idx) => (
                  <Grid item xs={12} key={idx}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          {prediction.description}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Probability: {(prediction.probability * 100).toFixed(1)}%
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Timing: {formatPredictionTiming(prediction.timing)}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
            </Grid>
          </TabPanel>
        ))}
      </Paper>
    </Container>
  );
};

export default PredictionsPage;
