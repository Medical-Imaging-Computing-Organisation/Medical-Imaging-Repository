//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
//
// $Id: B1PrimaryGeneratorAction.cc 94307 2015-11-11 13:42:46Z gcosmo $
//
/// \file B1PrimaryGeneratorAction.cc
/// \brief Implementation of the B1PrimaryGeneratorAction class

#include "B1PrimaryGeneratorAction.hh"

#include "G4LogicalVolumeStore.hh"
#include "G4LogicalVolume.hh"
#include "G4Box.hh"
#include "G4RunManager.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"
#include "G4SystemOfUnits.hh"
#include "Randomize.hh" 
#include <cmath> 

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1PrimaryGeneratorAction::B1PrimaryGeneratorAction()
: G4VUserPrimaryGeneratorAction(),
  fParticleGun(0), 
  fEnvelopeBox(0)
{
  G4int n_particle = 1;
  fParticleGun  = new G4ParticleGun(n_particle);

  // default particle kinematic
  G4ParticleTable* particleTable = G4ParticleTable::GetParticleTable();
  G4String particleName;
  G4ParticleDefinition* particle
    = particleTable->FindParticle(particleName="gamma");
  fParticleGun->SetParticleDefinition(particle);
  fParticleGun->SetParticleEnergy(662.*keV);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1PrimaryGeneratorAction::~B1PrimaryGeneratorAction()
{
  delete fParticleGun;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void B1PrimaryGeneratorAction::GeneratePrimaries(G4Event* anEvent)
{
  //this function is called at the begining of ecah event
  //

  // In order to avoid dependence of PrimaryGeneratorAction
  // on DetectorConstruction class we get Envelope volume
  // from G4LogicalVolumeStore.
  
  G4double XY = 1*cm;
  G4double Z = 0;

  G4double size = 1.0; 
  G4double x0 = size * XY * (G4UniformRand()-0.5);
  G4double y0 = size * XY * (G4UniformRand()-0.5);
  G4double z0 = -0.5 * Z;
  
  fParticleGun->SetParticlePosition(G4ThreeVector(x0,y0,z0));

  
  G4ThreeVector d1position = G4ThreeVector(20, 20, 20); 

  G4double d1size = 2.0; 


  G4double d1_r = d1position.mag(); 
  G4double d1_theta = d1position.theta(); 
  G4double d1_phi = d1position.phi(); 
  

  G4double d1_theta_max = d1size/d1_r;  
  G4double d1_phi_max = d1_theta_max; 
  
  std::cout << "Angular deviation in polar and azimuthial: " << d1_theta_max << " & " << d1_phi_max << std::endl;
  
  G4double polarAngle = d1_theta + 2*(G4UniformRand()-0.5)*d1_theta_max; 
  G4double azimuthialAngle = d1_phi + 2*(G4UniformRand()-0.5)*d1_phi_max;
  
  std::cout << "Random particle momentum in polar: Theta & Phi: " << polarAngle << " & " << azimuthialAngle << std::endl;
  
  G4double px = std::sin(polarAngle)*std::cos(azimuthialAngle); 
  G4double py = std::sin(polarAngle)*std::sin(azimuthialAngle); 
  G4double pz = std::cos(polarAngle);
  
  G4ThreeVector direction(px, py, pz); 
  
  std::cout << "Random particle momentum in cartesian after roation are: x, y & z: " << direction.x() << ", "<< direction.y() << " & "<< direction.z() << std::endl;
  
  fParticleGun->SetParticleMomentum(direction); 
  fParticleGun->SetParticleEnergy(662.*keV);

/*
 std::cout << "" << std::endl;
 std::cout << "---------------------------" << std::endl;
 std::cout << "" << std::endl;
*/

  fParticleGun->GeneratePrimaryVertex(anEvent);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
