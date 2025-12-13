local function normalize(r, g, b)
	return { r / 255, g / 255, b / 255 }
end

return {
	RED = normalize(210, 15, 57),
	GREEN = normalize(64, 160, 43),
	BLUE = normalize(30, 102, 245),
	BASE = normalize(30, 30, 46),
	CRUST = normalize(17, 17, 27),
	normalize = normalize,
}
