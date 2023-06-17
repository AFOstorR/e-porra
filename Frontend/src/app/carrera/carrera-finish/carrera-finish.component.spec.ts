/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { CarreraFinishComponent } from './carrera-finish.component';

describe('CarreraFinishComponent', () => {
  let component: CarreraFinishComponent;
  let fixture: ComponentFixture<CarreraFinishComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CarreraFinishComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CarreraFinishComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
