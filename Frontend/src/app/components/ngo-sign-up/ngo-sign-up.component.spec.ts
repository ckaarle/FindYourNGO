import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoSignUpComponent } from './ngo-sign-up.component';

describe('NgoSignUpComponent', () => {
  let component: NgoSignUpComponent;
  let fixture: ComponentFixture<NgoSignUpComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoSignUpComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoSignUpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
