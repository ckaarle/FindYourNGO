import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoDetailItemComponent } from './ngo-detail-item.component';

describe('NgoDetailItemComponent', () => {
  let component: NgoDetailItemComponent;
  let fixture: ComponentFixture<NgoDetailItemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoDetailItemComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoDetailItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
