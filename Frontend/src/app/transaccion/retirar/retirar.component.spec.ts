/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { RetirarComponent } from './retirar.component';

describe('UsuarioRetirarComponent', () => {
  let component: RetirarComponent;
  let fixture: ComponentFixture<RetirarComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RetirarComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RetirarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
