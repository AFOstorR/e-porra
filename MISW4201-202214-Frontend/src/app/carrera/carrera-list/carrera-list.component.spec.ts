/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { CarreraListComponent } from './carrera-list.component';

describe('CarreraListComponent', () => {
  let component: CarreraListComponent;
  let fixture: ComponentFixture<CarreraListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CarreraListComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CarreraListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
