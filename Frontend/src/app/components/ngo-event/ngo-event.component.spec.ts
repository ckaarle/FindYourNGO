import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoEventComponent } from './ngo-event.component';

describe('EventsScreenComponent', () => {
  let component: NgoEventComponent;
  let fixture: ComponentFixture<NgoEventComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoEventComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoEventComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
