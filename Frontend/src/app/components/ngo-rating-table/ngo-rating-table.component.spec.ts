import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoRatingTableComponent } from './ngo-rating-table.component';

describe('NgoRatingTableComponent', () => {
  let component: NgoRatingTableComponent;
  let fixture: ComponentFixture<NgoRatingTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoRatingTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoRatingTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
