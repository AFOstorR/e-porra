/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ApuestaEditComponent } from './apuesta-edit.component';

describe('ApuestaEditComponent', () => {
  let component: ApuestaEditComponent;
  let fixture: ComponentFixture<ApuestaEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ApuestaEditComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ApuestaEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
