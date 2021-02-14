import { TestBed } from '@angular/core/testing';

import { AutoscrollService } from './autoscroll.service';

describe('AutoscrollService', () => {
  let service: AutoscrollService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AutoscrollService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
