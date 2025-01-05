import React from 'react';
import {
  Menu,
  MenuItem,
  IconButton,
  Typography,
  Slider,
  Switch,
  FormControlLabel,
  Divider,
} from '@mui/material';
import { Accessibility } from '@mui/icons-material';
import { useAccessibility } from './AccessibilityProvider';

export const AccessibilityMenu: React.FC = () => {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const {
    fontSize,
    contrast,
    reducedMotion,
    screenReaderMode,
    setFontSize,
    setContrast,
    setReducedMotion,
    setScreenReaderMode,
  } = useAccessibility();

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <>
      <IconButton
        aria-label="accessibility options"
        onClick={handleClick}
        color="inherit"
      >
        <Accessibility />
      </IconButton>
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        PaperProps={{
          sx: { width: 320, p: 2 },
        }}
      >
        <Typography variant="h6" gutterBottom>
          Accessibility Options
        </Typography>
        <Divider sx={{ my: 1 }} />
        
        <Typography id="font-size-slider" gutterBottom>
          Font Size
        </Typography>
        <Slider
          value={fontSize}
          onChange={(_, value) => setFontSize(value as number)}
          aria-labelledby="font-size-slider"
          min={12}
          max={24}
          step={1}
          marks
          valueLabelDisplay="auto"
          sx={{ mb: 2 }}
        />

        <FormControlLabel
          control={
            <Switch
              checked={contrast === 'high'}
              onChange={(e) =>
                setContrast(e.target.checked ? 'high' : 'normal')
              }
            />
          }
          label="High Contrast"
        />

        <FormControlLabel
          control={
            <Switch
              checked={reducedMotion}
              onChange={(e) => setReducedMotion(e.target.checked)}
            />
          }
          label="Reduce Motion"
        />

        <FormControlLabel
          control={
            <Switch
              checked={screenReaderMode}
              onChange={(e) => setScreenReaderMode(e.target.checked)}
            />
          }
          label="Screen Reader Mode"
        />

        <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
          These settings will be saved for your next visit.
        </Typography>
      </Menu>
    </>
  );
};
