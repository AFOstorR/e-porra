/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { CarreraReportComponent } from './carrera-report.component';

describe('CarreraFinishComponent', () => {
  let component: CarreraReportComponent;
  let fixture: ComponentFixture<CarreraReportComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CarreraReportComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CarreraReportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
