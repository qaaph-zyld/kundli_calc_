import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Grid,
  Button,
  Stepper,
  Step,
  StepLabel,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import KundliForm from '../components/forms/KundliForm';
import KundliChart from '../components/charts/KundliChart';
import { kundliApi } from '../services/api';

interface MatchingResult {
  totalScore: number;
  aspects: {
    name: string;
    score: number;
    description: string;
    recommendation?: string;
  }[];
  compatibility: string;
  detailedAnalysis: string;
}

const steps = ['Person 1 Details', 'Person 2 Details', 'Results'];

const MatchingPage: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [person1Data, setPerson1Data] = useState<any>(null);
  const [person2Data, setPerson2Data] = useState<any>(null);
  const [matchingResult, setMatchingResult] = useState<MatchingResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePerson1Submit = (data: any) => {
    setPerson1Data(data);
    setActiveStep(1);
  };

  const handlePerson2Submit = async (data: any) => {
    setPerson2Data(data);
    try {
      setLoading(true);
      setError(null);
      const result = await kundliApi.calculateMatching({
        person1: person1Data,
        person2: data,
      });
      setMatchingResult(result);
      setActiveStep(2);
    } catch (err) {
      setError('Failed to calculate matching. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setActiveStep(0);
    setPerson1Data(null);
    setPerson2Data(null);
    setMatchingResult(null);
    setError(null);
  };

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Enter Person 1's Details
            </Typography>
            <KundliForm onSubmit={handlePerson1Submit} />
          </Box>
        );
      case 1:
        return (
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Enter Person 2's Details
            </Typography>
            <KundliForm onSubmit={handlePerson2Submit} />
          </Box>
        );
      case 2:
        return (
          <Box sx={{ mt: 3 }}>
            {matchingResult && (
              <>
                <Typography variant="h5" gutterBottom align="center">
                  Matching Score: {matchingResult.totalScore}/36
                </Typography>
                <Typography
                  variant="h6"
                  gutterBottom
                  align="center"
                  color="primary"
                >
                  {matchingResult.compatibility}
                </Typography>

                <Grid container spacing={4} sx={{ mt: 2 }}>
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" gutterBottom>
                      Person 1's Chart
                    </Typography>
                    {person1Data && (
                      <KundliChart
                        planets={person1Data.planets}
                        houses={person1Data.houses}
                      />
                    )}
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" gutterBottom>
                      Person 2's Chart
                    </Typography>
                    {person2Data && (
                      <KundliChart
                        planets={person2Data.planets}
                        houses={person2Data.houses}
                      />
                    )}
                  </Grid>
                </Grid>

                <Paper sx={{ p: 3, mt: 4 }}>
                  <Typography variant="h6" gutterBottom>
                    Detailed Analysis
                  </Typography>
                  <Typography paragraph>{matchingResult.detailedAnalysis}</Typography>

                  <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                    Aspect-wise Scores
                  </Typography>
                  <Grid container spacing={2}>
                    {matchingResult.aspects.map((aspect, index) => (
                      <Grid item xs={12} key={index}>
                        <Paper sx={{ p: 2 }}>
                          <Typography variant="subtitle1" gutterBottom>
                            {aspect.name} - {aspect.score} points
                          </Typography>
                          <Typography variant="body2" paragraph>
                            {aspect.description}
                          </Typography>
                          {aspect.recommendation && (
                            <Typography
                              variant="body2"
                              color="primary"
                              sx={{ mt: 1 }}
                            >
                              Recommendation: {aspect.recommendation}
                            </Typography>
                          )}
                        </Paper>
                      </Grid>
                    ))}
                  </Grid>
                </Paper>

                <Box sx={{ mt: 4, textAlign: 'center' }}>
                  <Button
                    variant="contained"
                    onClick={handleReset}
                    sx={{ minWidth: 200 }}
                  >
                    Calculate New Match
                  </Button>
                </Box>
              </>
            )}
          </Box>
        );
      default:
        return null;
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
          Kundli Matching
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {renderStepContent(activeStep)}
      </Paper>
    </Container>
  );
};

export default MatchingPage;
