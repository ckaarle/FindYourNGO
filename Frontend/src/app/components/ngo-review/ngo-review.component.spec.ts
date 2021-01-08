import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoReviewComponent } from './ngo-review.component';

describe('NgoReviewComponent', () => {
  let component: NgoReviewComponent;
  let fixture: ComponentFixture<NgoReviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoReviewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoReviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
