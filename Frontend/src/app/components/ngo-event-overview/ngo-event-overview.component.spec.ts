import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoEventOverviewComponent } from './ngo-event-overview.component';

describe('NgoEventOverviewComponent', () => {
  let component: NgoEventOverviewComponent;
  let fixture: ComponentFixture<NgoEventOverviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoEventOverviewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoEventOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
