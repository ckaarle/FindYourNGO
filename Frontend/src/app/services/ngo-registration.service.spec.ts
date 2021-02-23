import { TestBed } from '@angular/core/testing';

import { NgoRegistrationService } from './ngo-registration.service';

describe('NgoRegistrationService', () => {
  let service: NgoRegistrationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NgoRegistrationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
