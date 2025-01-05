import React from 'react';
import { Box, Typography, Container, Grid, Paper, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import {
  Calculate as CalculateIcon,
  Psychology as PsychologyIcon,
  Compare as CompareIcon,
  Timeline as TimelineIcon,
} from '@mui/icons-material';

const Home: React.FC = () => {
  const navigate = useNavigate();

  const features = [
    {
      title: 'Birth Chart Calculation',
      description: 'Calculate detailed birth charts with multiple house systems and ayanamsa options',
      icon: <CalculateIcon sx={{ fontSize: 40 }} />,
      action: () => navigate('/calculate'),
    },
    {
      title: 'Predictions & Analysis',
      description: 'Get personalized predictions and detailed astrological analysis',
      icon: <PsychologyIcon sx={{ fontSize: 40 }} />,
      action: () => navigate('/predictions'),
    },
    {
      title: 'Compatibility Matching',
      description: 'Check compatibility between two birth charts',
      icon: <CompareIcon sx={{ fontSize: 40 }} />,
      action: () => navigate('/matching'),
    },
    {
      title: 'Transit Analysis',
      description: 'Analyze planetary transits and their effects',
      icon: <TimelineIcon sx={{ fontSize: 40 }} />,
      action: () => navigate('/transit'),
    },
  ];

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography
          variant="h2"
          component="h1"
          gutterBottom
          align="center"
          sx={{ fontWeight: 'bold', mb: 6 }}
        >
          Advanced Kundli Calculator
        </Typography>

        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Paper
                sx={{
                  p: 3,
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  textAlign: 'center',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-5px)',
                  },
                }}
                elevation={3}
              >
                <Box sx={{ color: 'primary.main', mb: 2 }}>{feature.icon}</Box>
                <Typography variant="h6" component="h2" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{ mb: 2, flexGrow: 1 }}
                >
                  {feature.description}
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={feature.action}
                >
                  Try Now
                </Button>
              </Paper>
            </Grid>
          ))}
        </Grid>

        <Box sx={{ mt: 8, textAlign: 'center' }}>
          <Typography variant="h4" component="h2" gutterBottom>
            Why Choose Our Kundli Calculator?
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            Our advanced Kundli calculator combines traditional Vedic astrology with modern
            technology to provide accurate and detailed astrological calculations. With
            support for multiple ayanamsa systems, house systems, and comprehensive
            predictions, we offer one of the most complete astrological analysis tools
            available.
          </Typography>
          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={() => navigate('/calculate')}
            sx={{ mt: 2 }}
          >
            Get Started Now
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default Home;
