import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgoTwHistoryComponent } from './ngo-tw-history.component';

describe('NgoTwHistoryComponent', () => {
  let component: NgoTwHistoryComponent;
  let fixture: ComponentFixture<NgoTwHistoryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgoTwHistoryComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NgoTwHistoryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
