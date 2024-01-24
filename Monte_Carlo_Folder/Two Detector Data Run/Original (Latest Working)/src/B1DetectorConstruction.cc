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
// $Id: B1DetectorConstruction.cc 94307 2015-11-11 13:42:46Z gcosmo $
//
/// \file B1DetectorConstruction.cc
/// \brief Implementation of the B1DetectorConstruction class

#include "B1DetectorConstruction.hh"

#include "G4RunManager.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4Cons.hh"
#include "G4Orb.hh"
#include "G4Sphere.hh"
#include "G4Trd.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4Tubs.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1DetectorConstruction::B1DetectorConstruction()
: G4VUserDetectorConstruction(),
  fScoringVolume(0)
{ 


}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1DetectorConstruction::~B1DetectorConstruction()
{ }

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

G4VPhysicalVolume* B1DetectorConstruction::Construct()
{  
  // Get nist material manager
  G4NistManager* nist = G4NistManager::Instance();
  
  // Option to switch on/off checking of volumes overlaps
  //
  G4bool checkOverlaps = true;

  //     
  // World
  //
  G4double world_sizeXY = 50*cm;
  G4double world_sizeZ  = 0.5*m;
  G4Material* world_mat = nist->FindOrBuildMaterial("G4_AIR");
  
  G4Box* solidWorld = new G4Box("World",0.5*world_sizeXY, 0.5*world_sizeXY, 0.5*world_sizeZ);     //its size
      
  G4LogicalVolume* logicWorld = new G4LogicalVolume(solidWorld, world_mat, "World");            //its name
                                   
  G4VPhysicalVolume* physWorld = new G4PVPlacement(0,G4ThreeVector(),       //at (0,0,0)
                      logicWorld,            //its logical volume
                      "World",               //its name
                      0,                     //its mother  volume
                      false,                 //no boolean operation
                      0,                     //copy number
                      checkOverlaps);        //overlaps checking
  

	// create 2 in NaI crystal
	// note these dimensions are probably wrong!!
	G4double NaI_r = 2.34*cm;
	G4double NaI_hz = 2*cm;

	G4Tubs* NaI_shape = new G4Tubs("NaI", 0*mm, NaI_r, NaI_hz, 0*deg, 360*deg);
	
	G4LogicalVolume* NaI_log = new G4LogicalVolume(NaI_shape, nist->FindOrBuildMaterial("G4_SODIUM_IODIDE"), "NaI");

	G4RotationMatrix* absorber_rot = new G4RotationMatrix();
	absorber_rot->rotateX(0*deg);
	G4ThreeVector absorber_pos = G4ThreeVector(0,0,20*cm);
	G4VPhysicalVolume* NaI_absorber = new G4PVPlacement(absorber_rot, absorber_pos, "absorber", NaI_log, physWorld, false, 0, checkOverlaps);
/*
	G4Box* shape = new G4Box("shape", 1*mm,1*mm,1*mm);
	G4LogicalVolume* LV = new G4LogicalVolume(shape,world_mat,"LV");
		G4PVPlacement(0,G4ThreeVector(0,0*cm,0), LV,"PV", NaI_log, false,0,checkOverlaps);
*/

/*	G4ThreeVector scatterer_pos = G4ThreeVector(0,0,10*cm);
	G4VPhysicalVolume* NaI_scatterer = new G4PVPlacement(0, scatterer_pos, "scatterer", NaI_log, physWorld, false, 0, checkOverlaps);	
        G4VPhysicalVolume* NaI_scatterer2 = new G4PVPlacement(0, G4ThreeVector(0,0,-10*cm), "scatterer", NaI_log, physWorld, false, 1, checkOverlaps);
*/

 //
  //always return the physical World
  //
  return physWorld;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
