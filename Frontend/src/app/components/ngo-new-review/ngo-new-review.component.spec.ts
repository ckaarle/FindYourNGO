import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoNewReviewComponent } from './ngo-new-review.component';

describe('NgoNewReviewComponent', () => {
  let component: NgoNewReviewComponent;
  let fixture: ComponentFixture<NgoNewReviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoNewReviewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoNewReviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
