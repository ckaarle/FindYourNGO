import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoRatingComponent } from './ngo-rating.component';

describe('NgoRatingComponent', () => {
  let component: NgoRatingComponent;
  let fixture: ComponentFixture<NgoRatingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoRatingComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoRatingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
