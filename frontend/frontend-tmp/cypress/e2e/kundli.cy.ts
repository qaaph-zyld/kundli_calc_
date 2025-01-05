describe('Kundli Calculation Flow', () => {
  beforeEach(() => {
    cy.login('testuser', 'password123');
  });

  it('should navigate to calculate page', () => {
    cy.get('[data-testid="calculate-nav"]').click();
    cy.url().should('include', '/calculate');
  });

  it('should show validation errors on empty form submission', () => {
    cy.visit('/calculate');
    cy.get('[data-testid="calculate-submit"]').click();
    cy.contains('Date is required');
    cy.contains('Time is required');
    cy.contains('Latitude is required');
    cy.contains('Longitude is required');
  });

  it('should calculate kundli with valid data', () => {
    cy.visit('/calculate');
    
    // Fill form
    cy.get('[data-testid="date-input"]').type('2000-01-01');
    cy.get('[data-testid="time-input"]').type('12:00');
    cy.get('[data-testid="latitude-input"]').type('28.6139');
    cy.get('[data-testid="longitude-input"]').type('77.2090');
    cy.get('[data-testid="timezone-input"]').select('Asia/Kolkata');
    
    // Submit form
    cy.get('[data-testid="calculate-submit"]').click();
    
    // Check results
    cy.get('[data-testid="kundli-chart"]').should('exist');
    cy.get('[data-testid="planet-positions"]').should('exist');
    cy.contains('Kundli Chart');
  });

  it('should generate predictions for calculated kundli', () => {
    // Calculate kundli first
    cy.calculateKundli({
      date: '2000-01-01',
      time: '12:00',
      latitude: 28.6139,
      longitude: 77.2090,
      timezone: 'Asia/Kolkata',
    });
    
    // Navigate to predictions
    cy.get('[data-testid="predictions-tab"]').click();
    
    // Check predictions
    cy.get('[data-testid="prediction-cards"]').should('exist');
    cy.get('[data-testid="prediction-card"]').should('have.length.at.least', 1);
  });

  it('should save kundli for future reference', () => {
    // Calculate kundli
    cy.calculateKundli({
      date: '2000-01-01',
      time: '12:00',
      latitude: 28.6139,
      longitude: 77.2090,
      timezone: 'Asia/Kolkata',
    });
    
    // Save kundli
    cy.get('[data-testid="save-kundli"]').click();
    cy.contains('Kundli saved successfully');
    
    // Check saved kundlis
    cy.get('[data-testid="saved-kundlis"]').click();
    cy.get('[data-testid="kundli-list-item"]').should('have.length.at.least', 1);
  });
});
