import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoOwnReviewComponent } from './ngo-own-review.component';

describe('NgoOwnReviewComponent', () => {
  let component: NgoOwnReviewComponent;
  let fixture: ComponentFixture<NgoOwnReviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoOwnReviewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoOwnReviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
