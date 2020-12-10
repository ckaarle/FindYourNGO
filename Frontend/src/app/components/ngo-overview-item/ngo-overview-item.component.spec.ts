import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoOverviewItemComponent } from './ngo-overview-item.component';

describe('NgoOverviewItemComponent', () => {
  let component: NgoOverviewItemComponent;
  let fixture: ComponentFixture<NgoOverviewItemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoOverviewItemComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoOverviewItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
