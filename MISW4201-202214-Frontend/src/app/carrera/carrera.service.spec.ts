/* tslint:disable:no-unused-variable */

import { inject, TestBed } from '@angular/core/testing';
import { CarreraService } from './carrera.service';

describe('Service: Carrera', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CarreraService]
    });
  });

  it('should ...', inject([CarreraService], (service: CarreraService) => {
    expect(service).toBeTruthy();
  }));
});
