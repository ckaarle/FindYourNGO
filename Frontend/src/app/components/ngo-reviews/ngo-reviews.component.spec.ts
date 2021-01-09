import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoReviewsComponent } from './ngo-reviews.component';

describe('NgoReviewsComponent', () => {
  let component: NgoReviewsComponent;
  let fixture: ComponentFixture<NgoReviewsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoReviewsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoReviewsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
