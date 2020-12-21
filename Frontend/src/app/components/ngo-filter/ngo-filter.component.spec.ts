import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoFilterComponent } from './ngo-filter.component';

describe('NgoFilterComponent', () => {
  let component: NgoFilterComponent;
  let fixture: ComponentFixture<NgoFilterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoFilterComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
