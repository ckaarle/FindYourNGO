import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoTwRatingComponent } from './ngo-tw-rating.component';

describe('NgoTwRatingComponent', () => {
  let component: NgoTwRatingComponent;
  let fixture: ComponentFixture<NgoTwRatingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoTwRatingComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoTwRatingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
