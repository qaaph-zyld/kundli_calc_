import React from 'react';
import { useFormik } from 'formik';
import * as yup from 'yup';
import {
  Box,
  TextField,
  Button,
  Grid,
  MenuItem,
  Typography,
} from '@mui/material';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';

const validationSchema = yup.object({
  date: yup.date().required('Birth date is required'),
  time: yup.date().required('Birth time is required'),
  latitude: yup
    .number()
    .min(-90, 'Latitude must be between -90 and 90')
    .max(90, 'Latitude must be between -90 and 90')
    .required('Latitude is required'),
  longitude: yup
    .number()
    .min(-180, 'Longitude must be between -180 and 180')
    .max(180, 'Longitude must be between -180 and 180')
    .required('Longitude is required'),
  timezone: yup.string().required('Timezone is required'),
  ayanamsa: yup.string().required('Ayanamsa system is required'),
  houseSystem: yup.string().required('House system is required'),
});

const KundliForm: React.FC = () => {
  const formik = useFormik({
    initialValues: {
      date: new Date(),
      time: new Date(),
      latitude: 0,
      longitude: 0,
      timezone: 'UTC',
      ayanamsa: 'lahiri',
      houseSystem: 'placidus',
    },
    validationSchema: validationSchema,
    onSubmit: (values) => {
      console.log(values);
      // TODO: Handle form submission
    },
  });

  return (
    <Box component="form" onSubmit={formik.handleSubmit} sx={{ mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Birth Details
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6}>
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <DatePicker
              label="Birth Date"
              value={formik.values.date}
              onChange={(value) => formik.setFieldValue('date', value)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  fullWidth
                  error={formik.touched.date && Boolean(formik.errors.date)}
                  helperText={formik.touched.date && formik.errors.date}
                />
              )}
            />
          </LocalizationProvider>
        </Grid>
        <Grid item xs={12} sm={6}>
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <TimePicker
              label="Birth Time"
              value={formik.values.time}
              onChange={(value) => formik.setFieldValue('time', value)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  fullWidth
                  error={formik.touched.time && Boolean(formik.errors.time)}
                  helperText={formik.touched.time && formik.errors.time}
                />
              )}
            />
          </LocalizationProvider>
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            id="latitude"
            name="latitude"
            label="Latitude"
            type="number"
            value={formik.values.latitude}
            onChange={formik.handleChange}
            error={formik.touched.latitude && Boolean(formik.errors.latitude)}
            helperText={formik.touched.latitude && formik.errors.latitude}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            id="longitude"
            name="longitude"
            label="Longitude"
            type="number"
            value={formik.values.longitude}
            onChange={formik.handleChange}
            error={formik.touched.longitude && Boolean(formik.errors.longitude)}
            helperText={formik.touched.longitude && formik.errors.longitude}
          />
        </Grid>
        <Grid item xs={12} sm={4}>
          <TextField
            fullWidth
            id="timezone"
            name="timezone"
            label="Timezone"
            select
            value={formik.values.timezone}
            onChange={formik.handleChange}
            error={formik.touched.timezone && Boolean(formik.errors.timezone)}
            helperText={formik.touched.timezone && formik.errors.timezone}
          >
            <MenuItem value="UTC">UTC</MenuItem>
            <MenuItem value="Asia/Kolkata">Asia/Kolkata</MenuItem>
            {/* Add more timezone options */}
          </TextField>
        </Grid>
        <Grid item xs={12} sm={4}>
          <TextField
            fullWidth
            id="ayanamsa"
            name="ayanamsa"
            label="Ayanamsa System"
            select
            value={formik.values.ayanamsa}
            onChange={formik.handleChange}
            error={formik.touched.ayanamsa && Boolean(formik.errors.ayanamsa)}
            helperText={formik.touched.ayanamsa && formik.errors.ayanamsa}
          >
            <MenuItem value="lahiri">Lahiri</MenuItem>
            <MenuItem value="raman">Raman</MenuItem>
            <MenuItem value="krishnamurti">Krishnamurti</MenuItem>
          </TextField>
        </Grid>
        <Grid item xs={12} sm={4}>
          <TextField
            fullWidth
            id="houseSystem"
            name="houseSystem"
            label="House System"
            select
            value={formik.values.houseSystem}
            onChange={formik.handleChange}
            error={formik.touched.houseSystem && Boolean(formik.errors.houseSystem)}
            helperText={formik.touched.houseSystem && formik.errors.houseSystem}
          >
            <MenuItem value="placidus">Placidus</MenuItem>
            <MenuItem value="koch">Koch</MenuItem>
            <MenuItem value="equal">Equal House</MenuItem>
            <MenuItem value="whole_sign">Whole Sign</MenuItem>
          </TextField>
        </Grid>
      </Grid>
      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          size="large"
        >
          Calculate Kundli
        </Button>
      </Box>
    </Box>
  );
};

export default KundliForm;
