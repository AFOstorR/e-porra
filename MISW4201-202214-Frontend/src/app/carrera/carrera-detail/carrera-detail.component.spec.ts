/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { CarreraDetailComponent } from './carrera-detail.component';

describe('CarreraDetailComponent', () => {
  let component: CarreraDetailComponent;
  let fixture: ComponentFixture<CarreraDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CarreraDetailComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CarreraDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
