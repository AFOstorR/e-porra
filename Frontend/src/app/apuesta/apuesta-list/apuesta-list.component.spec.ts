/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ApuestaListComponent } from './apuesta-list.component';

describe('ApuestaListComponent', () => {
  let component: ApuestaListComponent;
  let fixture: ComponentFixture<ApuestaListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ApuestaListComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ApuestaListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
