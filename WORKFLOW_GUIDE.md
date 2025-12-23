# User Workflow Guide

## Overview

This guide outlines the user journey through the Kundli Calculator application, from initial data entry to comprehensive chart analysis.

---

## Primary User Flows

### 1. Quick Chart Generation (Basic User)

**Goal**: Generate birth chart with minimal friction

**Steps**:
1. **Landing Page** → "Create Your Kundli" CTA
2. **Birth Details Form**:
   - Date picker (calendar UI)
   - Time picker (24-hour with AM/PM toggle)
   - Location autocomplete (integrated with Google Places API)
   - Timezone auto-detected
3. **Chart Display**:
   - South Indian chart (default for Vedic)
   - Basic planetary positions
   - Ascendant highlighted
4. **Next Actions**:
   - Download PDF
   - View detailed analysis
   - Save to account (if logged in)

**Time to Complete**: ~2 minutes

---

### 2. Comprehensive Analysis (Advanced User)

**Goal**: Deep dive into all astrological aspects

**Wizard Flow**:

#### Step 1: Personal Information
- Name (optional)
- Date of Birth
- Time of Birth (with accuracy indicator: exact/approximate/unknown)
- Place of Birth (with map confirmation)

#### Step 2: Calculation Preferences
- Ayanamsa: Lahiri (default) / Raman / KP
- House System: Whole Sign (default) / Placidus / Equal
- Chart Style: South Indian / North Indian / Both

#### Step 3: Analysis Selection (Checkboxes)
**Core Calculations** (always included):
- Birth Chart (D1)
- Planetary Positions
- Houses & Cusps

**Extended Analysis** (select as needed):
- ☐ Divisional Charts (D9, D10, D12, D16, D20, D24, D30, D60)
- ☐ Dasha Systems (Vimshottari, Yogini, Ashtottari, Jaimini)
- ☐ Yogas (184 combinations)
- ☐ Ashtakavarga
- ☐ Shadbala
- ☐ Transits (current + upcoming)
- ☐ Predictions (next 12 months)
- ☐ Remedies & Recommendations

#### Step 4: Review & Generate
- Summary of selections
- Estimated generation time
- Option to save preferences for future use

#### Step 5: Results Dashboard
**Navigation Tabs**:
1. **Overview** - Key insights & summary
2. **Birth Chart** - Visual chart with interpretations
3. **Planets** - Detailed planetary analysis
4. **Houses** - House-wise breakdown
5. **Dashas** - Timeline view with periods
6. **Yogas** - All detected yogas with strength
7. **Transits** - Current & upcoming influences
8. **Vargas** - Divisional charts grid
9. **Reports** - Export options

---

### 3. Relationship Compatibility

**Goal**: Compare two birth charts for relationship insights

**Steps**:
1. **Entry Point**: "Compare Charts" or "Compatibility Analysis"
2. **Person 1 Details**:
   - Birth data (as in Flow #1)
   - Relationship role: Self / Partner / Friend / Family
3. **Person 2 Details**:
   - Same birth data collection
   - Relationship role confirmation
4. **Synastry Results**:
   - Compatibility score (0-100)
   - Key aspects visualization
   - Strengths & challenges
   - Relationship themes
   - Actionable advice
5. **Detailed Comparison**:
   - Side-by-side chart view
   - Inter-chart aspects table
   - Composite chart (optional advanced feature)

---

## Mobile-Responsive Considerations

### Mobile Flow Optimizations:
1. **Progressive Disclosure**: Show essentials first, expand details on tap
2. **Swipeable Charts**: Navigate between divisional charts by swiping
3. **Collapsible Sections**: Expand/collapse yogas, dashas, planetary details
4. **Quick Actions Bar**: Save, Share, Export always accessible
5. **Offline Mode**: Save chart data locally for offline viewing

### Mobile-Specific Features:
- Camera input for birth certificate OCR (future)
- Voice input for location names
- Push notifications for transit alerts
- Share directly to WhatsApp/social media

---

## Progressive Enhancement Strategy

### Level 1: Core Functionality (MVP)
- Birth chart generation
- Basic planetary positions
- House placements
- South Indian chart display

### Level 2: Intermediate Analysis
- Vimshottari dasha
- Major yogas (top 20)
- Divisional charts (D9)
- Current transits

### Level 3: Advanced Features
- All 184 yogas
- Multiple dasha systems
- All divisional charts
- Ashtakavarga & Shadbala
- KP System

### Level 4: Expert Tools
- Chart rectification
- Prashna (horary)
- Muhurta (electional)
- Relationship compatibility
- AI-powered predictions

---

## User Personalization

### Saved Preferences:
- Default ayanamsa & house system
- Preferred chart style
- Language preference (future: Hindi, Tamil, etc.)
- Favorite analysis modules
- Color theme (light/dark mode)

### User Profiles:
- Save multiple birth charts (self, family, friends)
- Chart collections ("Family", "Clients", etc.)
- Historical analysis tracking
- Bookmark specific yogas or dashas

---

## Error Handling & Edge Cases

### Invalid Input Handling:
1. **Unknown Birth Time**:
   - Offer solar chart (12:00 PM)
   - Explain limitations (no houses, no dasha)
   - Suggest chart rectification service

2. **Ambiguous Location**:
   - Show multiple matches on map
   - Allow manual lat/long entry
   - Validate timezone consistency

3. **Extreme Coordinates**:
   - Handle polar regions gracefully
   - Show midnight sun warnings
   - Explain potential calculation limitations

### Network Issues:
- Offline mode for saved charts
- Graceful degradation (show cached data)
- Clear "Retrying..." feedback

---

## Accessibility Features

### Screen Reader Support:
- All charts have text descriptions
- Planetary positions read as "Sun in Leo at 15 degrees"
- Yoga descriptions fully accessible

### Keyboard Navigation:
- Tab through all interactive elements
- Shortcuts: C for Chart, D for Dashas, Y for Yogas
- Escape to close modals

### Visual Accommodations:
- High contrast mode
- Adjustable font sizes
- Color-blind friendly palettes
- Reduced motion option

---

## Onboarding & Help

### First-Time User Flow:
1. **Welcome Screen**: 3 slides explaining the app
2. **Sample Chart**: Pre-populated with famous person data
3. **Interactive Tour**: Highlight key features (optional)
4. **Video Tutorial**: 2-minute overview (embedded)

### Contextual Help:
- Tooltips on hover (desktop) / tap (mobile)
- "What is this?" links for technical terms
- Glossary of astrological terms
- FAQ section

### Support Channels:
- In-app chat (for logged-in users)
- Email support
- Community forum (future)
- Video tutorials library

---

## Export & Sharing Options

### Export Formats:
1. **PDF Report**:
   - Beautifully formatted
   - Includes all selected analyses
   - Branded with logo
   - Printable

2. **Image (PNG/JPG)**:
   - Chart snapshot
   - Social media optimized
   - Watermarked option

3. **JSON Data**:
   - For developers/advanced users
   - All calculation results
   - Import into other tools

### Sharing:
- Unique shareable URL (privacy-controlled)
- QR code for in-person sharing
- Social media templates
- Email directly from app

---

## Performance Benchmarks

### Target Load Times:
- Initial page load: < 2 seconds
- Chart generation: < 5 seconds
- Full analysis (all features): < 15 seconds
- Chart switching (D1→D9): < 500ms

### Optimization Strategies:
- Lazy load divisional charts
- Prefetch likely next actions
- Cache frequently accessed charts
- Progressive image loading

---

## Wizard Mode Implementation Notes

### Frontend State Management:
```javascript
// Step flow state
const wizardSteps = [
  { id: 1, name: "Personal Info", complete: false },
  { id: 2, name: "Preferences", complete: false },
  { id: 3, name: "Analysis Options", complete: false },
  { id: 4, name: "Review", complete: false }
];

// Validation per step
const validateStep = (stepId, formData) => {
  switch(stepId) {
    case 1: return validateBirthDetails(formData);
    case 2: return validatePreferences(formData);
    case 3: return true; // Optional selections
    case 4: return true;  // Review only
  }
};
```

### Backend API Endpoints:
- POST `/api/v1/wizard/start` - Initialize wizard session
- PUT `/api/v1/wizard/step/{stepId}` - Save step data
- POST `/api/v1/wizard/generate` - Generate full analysis
- GET `/api/v1/wizard/progress` - Retrieve saved progress

### Progress Persistence:
- LocalStorage for anonymous users
- Database for logged-in users
- Expire after 24 hours if incomplete
- Resume from any step

---

## Future Enhancements

### Planned Features:
1. **AI Chat Assistant**: "Ask about my chart"
2. **Voice Narration**: Audio playback of interpretations
3. **Animated Transits**: Watch planets move over time
4. **Comparative Analysis**: Compare across date ranges
5. **Mobile App**: Native iOS/Android apps
6. **Multi-Language**: Hindi, Tamil, Telugu, Kannada, etc.
7. **Regional Variations**: Tamil, Kerala, Bengali systems
8. **Live Consultation Booking**: Connect with astrologers

### Integration Opportunities:
- Google Calendar (transit alerts)
- Apple Health (track life events)
- Notion/Evernote (export reports)
- Zapier (automate workflows)

---

This workflow guide ensures a smooth, intuitive user experience from first visit to expert-level analysis, while maintaining astrological accuracy and respecting user preferences.
