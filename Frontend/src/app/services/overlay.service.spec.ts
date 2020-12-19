import { TestBed } from '@angular/core/testing';

import { NgoDetailItemService } from './ngo-detail-item.service';

describe('NgoDetailItemService', () => {
  let service: NgoDetailItemService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NgoDetailItemService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
