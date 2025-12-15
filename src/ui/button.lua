local Color = require("src.ui.colors")

---@class Button
---@field x number x coordinate
---@field y number y coordinate
---@field width number width of button
---@field height number height of button
---@field color table
---@field text string? text of button
---@field image love.Image? image
---@field action_f function
---@field was_pressed boolean
---@field is_hovered boolean
local Button = { was_pressed = false }

function Button:new(opts)
  opts = opts or {}
  opts.width = opts.width or 0
  opts.height = opts.height or 0
  opts.color = opts.color or Color.BLUE

  setmetatable(opts, self)
  self.__index = self
  return opts
end

--- Draw button
function Button:draw()
  local r, g, b = unpack(self.color)
  local a = self.is_hovered and 0.7 or 1
  love.graphics.setColor(r, g, b, a)

  local margin = 15
  local content = love.graphics.newTextBatch(love.graphics.getFont(), self.text) or self.image

  if content then
    local c_width, c_height = content:getWidth(), content:getHeight()
    self.width = c_width + margin
    self.height = c_height + margin

    love.graphics.rectangle("fill", self.x, self.y, self.width, self.height)
    love.graphics.setColor(1, 1, 1, 1)
    love.graphics.draw(content, self.x + margin / 2, self.y + margin / 2)
  end
end

--- Update button. Used for hovered effect.
function Button:update()
  local mx, my = love.mouse.getPosition()
  local hovered = mx >= self.x and mx <= self.x + self.width and my >= self.y and my <= self.y + self.height

  if hovered and love.mouse.isDown(1) and not self.was_pressed then
    self.was_pressed = true
    self.action_f()
  elseif not love.mouse.isDown(1) then
    self.was_pressed = false
  end

  self.is_hovered = hovered
end

return Button
