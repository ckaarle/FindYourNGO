import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoFilterSelectionComponent } from './ngo-filter-selection.component';

describe('NgoFilterSelectionComponent', () => {
  let component: NgoFilterSelectionComponent;
  let fixture: ComponentFixture<NgoFilterSelectionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoFilterSelectionComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoFilterSelectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
