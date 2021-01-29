import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoConnectionComponent } from './ngo-connection.component';

describe('NgoConnectionComponent', () => {
  let component: NgoConnectionComponent;
  let fixture: ComponentFixture<NgoConnectionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoConnectionComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoConnectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
