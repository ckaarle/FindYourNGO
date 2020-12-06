import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchScreenComponent } from './search-screen.component';

describe('SearchScreenComponent', () => {
  let component: SearchScreenComponent;
  let fixture: ComponentFixture<SearchScreenComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SearchScreenComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchScreenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
