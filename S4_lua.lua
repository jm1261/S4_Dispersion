S = S4.NewSimulation()
pcall(loadstring(S4.arg))
S:SetLattice({period, 0}, {0, period})
S:SetNumG(harmonics)
S:AddMaterial('mat1', {((mat1_n*mat1_n)-(mat1_k*mat1_k)), (2*mat1_n*mat1_k)})
S:AddMaterial('mat2', {((mat2_n * mat2_n)-(mat2_k)), (2*mat2_n*mat2_k)})
S:AddMaterial('mat3', {((mat3_n * mat3_n)-(mat3_k*mat3_k)), (2*mat3_n*mat3_k)})
S:AddLayer('top', mat1_thick, 'mat1')
S:AddLayer('middle', mat2_thick, 'mat2')
S:AddLayer('bottom', mat3_thick, 'mat3')
S:SetLayerPatternCircle(
		'middle',
		'mat1',
		{0, 0},
		hole_radius
)
S:SetExcitationPlanewave(
	{0, 0}, -- phi in [0,180), theta in [0,360)   --
		{1, 0}, -- s-polarization amp,phase degrees-
		{0, 0}) -- p-polarization                 --
freq = 1/wavelength
S:SetFrequency(freq)
transmission = S:GetPowerFlux('bottom')
inc, reflection = S:GetPowerFlux('top', 10)
print(wavelength, transmission, -reflection)
