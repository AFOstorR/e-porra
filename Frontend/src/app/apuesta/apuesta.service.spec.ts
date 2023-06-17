/* tslint:disable:no-unused-variable */

import { inject, TestBed } from '@angular/core/testing';
import { ApuestaService } from './apuesta.service';

describe('Service: Apuesta', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ApuestaService]
    });
  });

  it('should ...', inject([ApuestaService], (service: ApuestaService) => {
    expect(service).toBeTruthy();
  }));
});
