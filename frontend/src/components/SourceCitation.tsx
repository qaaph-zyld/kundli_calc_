/**
 * Source Citation Component
 * =========================
 * 
 * Displays classical text source citations with expandable verse details.
 * Shows chapter, verse, translation, and allows deep-dive into original texts.
 * 
 * Features:
 * - Expandable citation cards
 * - Color-coded by source (BPHS=blue, Saravali=green, Phaladeepika=purple)
 * - Verse-level attribution
 * - Translation display
 * - Link to full chapter (future feature)
 */

import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Chip,
  IconButton,
  Collapse,
  Box,
  Stack,
  Tooltip
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  MenuBook as BookIcon,
  Verified as VerifiedIcon
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';

interface SourceData {
  text: string;
  chapter: number;
  verses: string;
  translation?: string;
  translator?: string;
  edition?: string;
}

interface SourceCitationProps {
  source: SourceData;
  sourceName: 'BPHS' | 'Saravali' | 'Phaladeepika' | 'Jataka Parijata';
  compact?: boolean;
}

const ExpandButton = styled((props: any) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
  transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));

const sourceColors: Record<string, string> = {
  BPHS: '#1976d2',          // Blue
  Saravali: '#2e7d32',      // Green
  Phaladeepika: '#7b1fa2',  // Purple
  'Jataka Parijata': '#d84315'  // Deep Orange
};

export const SourceCitation: React.FC<SourceCitationProps> = ({
  source,
  sourceName,
  compact = false
}) => {
  const [expanded, setExpanded] = useState(false);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const sourceColor = sourceColors[sourceName] || '#666';

  return (
    <Card
      variant="outlined"
      sx={{
        borderLeft: `4px solid ${sourceColor}`,
        mb: 1,
        backgroundColor: expanded ? 'rgba(0,0,0,0.02)' : 'white'
      }}
    >
      <CardContent sx={{ p: compact ? 1.5 : 2, '&:last-child': { pb: compact ? 1.5 : 2 } }}>
        <Stack direction="row" spacing={1} alignItems="center">
          <BookIcon sx={{ color: sourceColor, fontSize: compact ? 20 : 24 }} />
          
          <Box sx={{ flexGrow: 1 }}>
            <Stack direction="row" spacing={1} alignItems="center" flexWrap="wrap">
              <Tooltip title="Classical Text Source - Verified">
                <Chip
                  icon={<VerifiedIcon />}
                  label={sourceName}
                  size={compact ? "small" : "medium"}
                  sx={{
                    backgroundColor: sourceColor,
                    color: 'white',
                    fontWeight: 600
                  }}
                />
              </Tooltip>
              
              <Typography variant={compact ? "caption" : "body2"} color="text.secondary">
                Chapter {source.chapter}, Verses {source.verses}
              </Typography>
            </Stack>

            {!compact && source.translator && (
              <Typography variant="caption" color="text.secondary" display="block" mt={0.5}>
                Translation: {source.translator} ({source.edition})
              </Typography>
            )}
          </Box>

          {source.translation && (
            <Tooltip title={expanded ? "Hide translation" : "Show translation"}>
              <ExpandButton
                expand={expanded}
                onClick={handleExpandClick}
                aria-expanded={expanded}
                aria-label="show translation"
                size={compact ? "small" : "medium"}
              >
                <ExpandMoreIcon />
              </ExpandButton>
            </Tooltip>
          )}
        </Stack>

        {source.translation && (
          <Collapse in={expanded} timeout="auto" unmountOnExit>
            <Box
              sx={{
                mt: 2,
                p: 2,
                backgroundColor: 'rgba(0,0,0,0.03)',
                borderRadius: 1,
                borderLeft: `3px solid ${sourceColor}`
              }}
            >
              <Typography variant="body2" color="text.secondary" fontStyle="italic" paragraph>
                Classical Verse Translation:
              </Typography>
              <Typography variant="body2" sx={{ lineHeight: 1.7 }}>
                "{source.translation}"
              </Typography>
              
              {source.translator && (
                <Typography variant="caption" color="text.secondary" display="block" mt={1}>
                  — {source.translator}
                </Typography>
              )}
            </Box>
          </Collapse>
        )}
      </CardContent>
    </Card>
  );
};

/**
 * Multiple Source Citations Component
 * Shows multiple sources at once for comparison
 */
interface MultipleSourceCitationsProps {
  sources: Array<{
    sourceName: 'BPHS' | 'Saravali' | 'Phaladeepika' | 'Jataka Parijata';
    data: SourceData;
  }>;
  title?: string;
}

export const MultipleSourceCitations: React.FC<MultipleSourceCitationsProps> = ({
  sources,
  title = "Classical Sources"
}) => {
  return (
    <Box>
      {title && (
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <BookIcon />
          {title}
          <Chip
            label={`${sources.length} source${sources.length > 1 ? 's' : ''}`}
            size="small"
            color="primary"
            variant="outlined"
          />
        </Typography>
      )}
      
      <Stack spacing={1}>
        {sources.map((item, index) => (
          <SourceCitation
            key={index}
            source={item.data}
            sourceName={item.sourceName}
          />
        ))}
      </Stack>
    </Box>
  );
};

export default SourceCitation;
