local Color = require("src.ui.colors")

---@class Button
---@field x number x coordinate
---@field y number y coordinate
---@field text string? text of button
---@field image love.Image? image
local Button = {
	x = 0,
	y = 0,
	text = nil,
	image = nil,
}

function Button:new(opts)
	opts = opts or {}
	-- opts.content = love.graphics.newText(love.graphics.getFont(), "Button")

	setmetatable(opts, self)
	self.__index = self
	return opts
end

--- Draw button
function Button:draw()
	love.graphics.setColor(Color.BLUE)

	local margin = 15
	local content = love.graphics.newText(love.graphics.getFont(), self.text) or self.image
	local c_width, c_height = content:getWidth(), content:getHeight()

	love.graphics.rectangle("fill", self.x, self.y, c_width + margin, c_height + margin, 10, 10)
	love.graphics.setColor(1, 1, 1, 1)
	love.graphics.draw(content, self.x + margin / 2, self.y + margin / 2)
end

return Button
