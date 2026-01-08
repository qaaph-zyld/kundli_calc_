/**
 * Multi-Source Comparison Component
 * ==================================
 * 
 * Displays side-by-side comparison of interpretations from multiple classical texts.
 * Shows agreement levels, common themes, and unique perspectives.
 * 
 * Features:
 * - Agreement level visualization
 * - Common themes extraction
 * - Unique perspectives per source
 * - Synthesis view
 * - Source confidence scoring
 */

import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Chip,
  Box,
  Stack,
  Grid,
  LinearProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
  Alert
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  CheckCircle as AgreeIcon,
  Info as InfoIcon,
  Warning as DisagreeIcon,
  Lightbulb as ThemeIcon,
  AutoAwesome as SynthesisIcon
} from '@mui/icons-material';

interface SourceInterpretation {
  sourceName: string;
  interpretation: string;
  chapter: number;
  verses: string;
  confidence: number;
}

interface ComparisonData {
  planet: string;
  house: number;
  sources: SourceInterpretation[];
  agreementLevel: 'strong_agreement' | 'moderate_agreement' | 'neutral' | 'moderate_disagreement' | 'strong_disagreement';
  commonThemes: string[];
  uniquePerspectives: Array<{
    source: string;
    perspective: string;
  }>;
  synthesis: string;
  overallConfidence: number;
}

interface MultiSourceComparisonProps {
  data: ComparisonData;
}

const agreementConfig = {
  strong_agreement: {
    color: '#2e7d32',
    label: 'Strong Agreement',
    icon: <AgreeIcon />,
    description: 'Classical texts strongly agree on interpretation'
  },
  moderate_agreement: {
    color: '#558b2f',
    label: 'Moderate Agreement',
    icon: <AgreeIcon />,
    description: 'Texts generally agree with minor variations'
  },
  neutral: {
    color: '#ff9800',
    label: 'Neutral',
    icon: <InfoIcon />,
    description: 'Texts provide complementary perspectives'
  },
  moderate_disagreement: {
    color: '#f57c00',
    label: 'Moderate Disagreement',
    icon: <DisagreeIcon />,
    description: 'Texts show some conflicting views'
  },
  strong_disagreement: {
    color: '#d32f2f',
    label: 'Strong Disagreement',
    icon: <DisagreeIcon />,
    description: 'Significant differences between texts'
  }
};

export const MultiSourceComparison: React.FC<MultiSourceComparisonProps> = ({ data }) => {
  const [expanded, setExpanded] = useState<string | false>('synthesis');

  const handleChange = (panel: string) => (event: React.SyntheticEvent, isExpanded: boolean) => {
    setExpanded(isExpanded ? panel : false);
  };

  const agreement = agreementConfig[data.agreementLevel];

  return (
    <Card elevation={2}>
      <CardContent>
        {/* Header */}
        <Stack direction="row" spacing={2} alignItems="center" mb={3}>
          <Box>
            <Typography variant="h6" gutterBottom>
              Multi-Source Analysis: {data.planet} in {data.house}th House
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Comparing {data.sources.length} classical texts
            </Typography>
          </Box>
        </Stack>

        {/* Agreement Level */}
        <Box mb={3}>
          <Stack direction="row" spacing={1} alignItems="center" mb={1}>
            <Box sx={{ color: agreement.color }}>{agreement.icon}</Box>
            <Typography variant="subtitle1" fontWeight={600}>
              Agreement Level: {agreement.label}
            </Typography>
            <Chip
              label={`${Math.round(data.overallConfidence * 100)}% confidence`}
              size="small"
              color="primary"
            />
          </Stack>
          
          <LinearProgress
            variant="determinate"
            value={data.overallConfidence * 100}
            sx={{
              height: 8,
              borderRadius: 4,
              backgroundColor: 'rgba(0,0,0,0.1)',
              '& .MuiLinearProgress-bar': {
                backgroundColor: agreement.color
              }
            }}
          />
          
          <Typography variant="caption" color="text.secondary" mt={0.5} display="block">
            {agreement.description}
          </Typography>
        </Box>

        {/* Synthesis */}
        <Accordion expanded={expanded === 'synthesis'} onChange={handleChange('synthesis')}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Stack direction="row" spacing={1} alignItems="center">
              <SynthesisIcon color="primary" />
              <Typography variant="subtitle1" fontWeight={600}>
                Synthesized Interpretation
              </Typography>
            </Stack>
          </AccordionSummary>
          <AccordionDetails>
            <Alert severity="info" icon={<SynthesisIcon />} sx={{ mb: 2 }}>
              Combined wisdom from {data.sources.length} classical sources with verse-level attribution
            </Alert>
            <Typography variant="body1" sx={{ lineHeight: 1.8 }}>
              {data.synthesis}
            </Typography>
          </AccordionDetails>
        </Accordion>

        {/* Common Themes */}
        {data.commonThemes.length > 0 && (
          <Accordion expanded={expanded === 'themes'} onChange={handleChange('themes')}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Stack direction="row" spacing={1} alignItems="center">
                <ThemeIcon color="secondary" />
                <Typography variant="subtitle1" fontWeight={600}>
                  Common Themes ({data.commonThemes.length})
                </Typography>
              </Stack>
            </AccordionSummary>
            <AccordionDetails>
              <Stack spacing={1}>
                {data.commonThemes.map((theme, index) => (
                  <Chip
                    key={index}
                    label={theme}
                    color="secondary"
                    variant="outlined"
                    icon={<ThemeIcon />}
                  />
                ))}
              </Stack>
            </AccordionDetails>
          </Accordion>
        )}

        {/* Individual Sources */}
        <Accordion expanded={expanded === 'sources'} onChange={handleChange('sources')}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography variant="subtitle1" fontWeight={600}>
              Individual Source Interpretations ({data.sources.length})
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Grid container spacing={2}>
              {data.sources.map((source, index) => (
                <Grid item xs={12} md={6} key={index}>
                  <Card variant="outlined">
                    <CardContent>
                      <Stack direction="row" spacing={1} alignItems="center" mb={1}>
                        <Typography variant="subtitle2" fontWeight={600}>
                          {source.sourceName}
                        </Typography>
                        <Chip
                          label={`${Math.round(source.confidence * 100)}%`}
                          size="small"
                          color={source.confidence > 0.9 ? 'success' : 'default'}
                        />
                      </Stack>
                      
                      <Typography variant="caption" color="text.secondary" display="block" mb={1}>
                        Ch. {source.chapter}, Verses {source.verses}
                      </Typography>
                      
                      <Divider sx={{ my: 1 }} />
                      
                      <Typography variant="body2" sx={{ lineHeight: 1.6 }}>
                        {source.interpretation}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </AccordionDetails>
        </Accordion>

        {/* Unique Perspectives */}
        {data.uniquePerspectives.length > 0 && (
          <Accordion expanded={expanded === 'unique'} onChange={handleChange('unique')}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="subtitle1" fontWeight={600}>
                Unique Perspectives ({data.uniquePerspectives.length})
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Stack spacing={2}>
                {data.uniquePerspectives.map((item, index) => (
                  <Box key={index}>
                    <Typography variant="subtitle2" color="primary" gutterBottom>
                      {item.source} adds:
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {item.perspective}
                    </Typography>
                  </Box>
                ))}
              </Stack>
            </AccordionDetails>
          </Accordion>
        )}
      </CardContent>
    </Card>
  );
};

export default MultiSourceComparison;
