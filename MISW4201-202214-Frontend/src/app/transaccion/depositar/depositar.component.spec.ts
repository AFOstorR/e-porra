/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { DepositarComponent } from './depositar.component';

describe('DepositarComponent', () => {
  let component: DepositarComponent;
  let fixture: ComponentFixture<DepositarComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DepositarComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DepositarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
